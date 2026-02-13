"""指定期間の仕訳一覧を表示する。"""

import argparse
import sys

from client import request


def get_journals(start_date, end_date):
    accounts = request("get", "/accounts")
    acc_map = {a["entity_id"]: a["name"] for a in accounts}

    journals = request("get", "/journals", params={"start_date": start_date, "end_date": end_date})
    journals.sort(key=lambda j: j["journal_date"])

    return journals, acc_map


def format_journal(j, acc_map):
    lines = j["lines"]
    debits = [l for l in lines if l["side"] == "debit"]
    credits = [l for l in lines if l["side"] == "credit"]
    evidence = "📎" if j.get("evidence_ids") else "  "

    if len(debits) == 1 and len(credits) == 1:
        dr_name = acc_map.get(debits[0]["account_id"], f"?{debits[0]['account_id']}")
        cr_name = acc_map.get(credits[0]["account_id"], f"?{credits[0]['account_id']}")
        amount = debits[0]["amount"]
        return [f"{j['entity_id']:>6} | {j['journal_date']} | {evidence} | {j['description'][:30]:<30} | {dr_name:<12} / {cr_name:<12} | {amount:>10,}"]
    else:
        # 複合仕訳
        rows = [f"{j['entity_id']:>6} | {j['journal_date']} | {evidence} | {j['description'][:30]:<30} |"]
        for d in debits:
            name = acc_map.get(d["account_id"], f"?{d['account_id']}")
            rows.append(f"{'':>6} | {'':>10} |    |   {'':30} |   借方 {name:<12} {d['amount']:>10,}")
        for c in credits:
            name = acc_map.get(c["account_id"], f"?{c['account_id']}")
            rows.append(f"{'':>6} | {'':>10} |    |   {'':30} |   貸方 {name:<12} {c['amount']:>10,}")
        return rows


def main():
    parser = argparse.ArgumentParser(description="仕訳一覧を取得")
    parser.add_argument("start_date", help="開始日 (YYYY-MM-DD)")
    parser.add_argument("end_date", help="終了日 (YYYY-MM-DD)")
    args = parser.parse_args()

    try:
        journals, acc_map = get_journals(args.start_date, args.end_date)
        print(f"\n仕訳一覧: {args.start_date} 〜 {args.end_date} ({len(journals)} 件)")
        print("-" * 110)
        print(f"{'EID':>6} | {'Date':<10} | EV | {'Description':<30} | {'Debit / Credit':<27} | {'Amount':>10}")
        print("-" * 110)

        for j in journals:
            for row in format_journal(j, acc_map):
                print(row)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

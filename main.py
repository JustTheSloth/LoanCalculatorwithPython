import argparse
import math

def main():
    parser = argparse.ArgumentParser(description="Loan Calculator")
    parser.add_argument("--type", help="Type of payment: 'annuity' or 'diff'")
    parser.add_argument("--payment", type=float, help="Monthly payment amount")
    parser.add_argument("--principal", type=float, help="Loan principal")
    parser.add_argument("--periods", type=int, help="Number of periods (months)")
    parser.add_argument("--interest", type=float, help="Annual interest rate (as a percentage)")

    args = parser.parse_args()

    # Validate input
    if args.type not in ["annuity", "diff"] or args.interest is None:
        print("Incorrect parameters")
        return

    if args.type == "diff" and args.payment is not None:
        print("Incorrect parameters")
        return

    if args.interest <= 0 or (args.payment and args.payment <= 0) or (args.principal and args.principal <= 0) or (args.periods and args.periods <= 0):
        print("Incorrect parameters")
        return

    # Calculate nominal interest rate
    nominal_interest = args.interest / (12 * 100)

    if args.type == "annuity":
        if args.principal is None:
            # Calculate principal
            principal = math.floor(
                args.payment /
                ((nominal_interest * math.pow(1 + nominal_interest, args.periods)) /
                 (math.pow(1 + nominal_interest, args.periods) - 1))
            )
            overpayment = args.payment * args.periods - principal
            print(f"Your loan principal = {principal}!")
            print(f"Overpayment = {overpayment}")
        elif args.payment is None:
            # Calculate annuity payment
            annuity_payment = math.ceil(
                args.principal *
                (nominal_interest * math.pow(1 + nominal_interest, args.periods)) /
                (math.pow(1 + nominal_interest, args.periods) - 1)
            )
            overpayment = annuity_payment * args.periods - args.principal
            print(f"Your annuity payment = {annuity_payment}!")
            print(f"Overpayment = {overpayment}")
        elif args.periods is None:
            # Calculate number of periods
            periods = math.ceil(
                math.log(args.payment / (args.payment - nominal_interest * args.principal), 1 + nominal_interest)
            )
            years, months = divmod(periods, 12)
            time_str = f"{years} years" if years > 0 else ""
            if months > 0:
                time_str += f" and {months} months" if time_str else f"{months} months"
            print(f"It will take {time_str} to repay this loan!")
            overpayment = args.payment * periods - args.principal
            print(f"Overpayment = {overpayment}")
        else:
            print("Incorrect parameters")
    elif args.type == "diff":
        if args.principal is not None and args.periods is not None:
            total_payment = 0
            for m in range(1, args.periods + 1):
                diff_payment = math.ceil(
                    args.principal / args.periods +
                    nominal_interest * (args.principal - (args.principal * (m - 1) / args.periods))
                )
                total_payment += diff_payment
                print(f"Month {m}: payment is {diff_payment}")
            overpayment = total_payment - args.principal
            print(f"Overpayment = {overpayment}")
        else:
            print("Incorrect parameters")

main()
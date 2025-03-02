import argparse
from expense_tracker.services.category_service import add_category, view_categories, edit_category, delete_category
from expense_tracker.services.expense_service import add_expense, view_expenses, edit_expense, delete_expense

def main():
    parser = argparse.ArgumentParser(description='Expense Tracker CLI')
    subparsers = parser.add_subparsers(dest='command')


    help_main = subparsers.add_parser('--help')

    view_categories_parser = subparsers.add_parser('view-categories')

    add_category_parser = subparsers.add_parser('add-category')
    add_category_parser.add_argument('--name', type=str, required=True, help='Categoty name')

    edit_category_parser = subparsers.add_parser('edit-category')
    edit_category_parser.add_argument('--initial_name', type=str, required=True, help='Categoty name you want to rename')
    edit_category_parser.add_argument('--needed_name', type=str, required=True, help='Desired new name of category')

    delete_category_parser = subparsers.add_parser('delete-category')
    delete_category_parser.add_argument('--name', type=str, required=True, help='Name of the category to delete')

    add_expense_parser = subparsers.add_parser('add-expense')
    add_expense_parser.add_argument('--name', type=str, required=True, help='Header of expence')
    add_expense_parser.add_argument('--amount', type=float, required=True, help='Expense amount')
    add_expense_parser.add_argument('--category', type=str, required=True, help='Category name')
    add_expense_parser.add_argument('--description', type=str, required=False, help='Full description')

    view_expenses_parser = subparsers.add_parser('view-expenses')
    view_expenses_parser.add_argument('number', type=int, help='View last n expenses')
    view_expenses_parser.add_argument('category', type=str, help='To discover all available categories use command: \n view categories')


    edit_expense_parser = subparsers.add_parser('edit-expense')


    delete_expense_parser = subparsers.add_parser('delete-expense')
    delete_expense_parser.add_argument("--all", action="store_true", required=False, help="Option to delete all occurencies with given options. It is should be used only if you want to delete all records of certain category, time, etc.")
    delete_expense_parser.add_argument("--id", type=int, required=False, help="Id of the record you want to delete")
    delete_expense_parser.add_argument("--name", type=str, required=False, help="Id of the record/s you want to delete")
    delete_expense_parser.add_argument("--amount", type=float, required=False, help="Id of the record/s you want to delete")
    delete_expense_parser.add_argument("--time", type=str, required=False, help="Id of the record/s you want to delete")
    delete_expense_parser.add_argument("--category", type=str, required=False, help="Id of the record/s you want to delete")
    delete_expense_parser.add_argument("--description", type=str, required=False, help="Id of the record/s you want to delete")

    args = parser.parse_args()

    if args.command == 'add-category':
        add_category(args.name)
    elif args.command == 'view-categories':
        view_categories()
    elif args.command == 'delete-category':
        delete_category(args.name)
    elif args.command == 'edit-category':
        edit_category(args.initial_name, args.needed_name)
    elif args.command == 'add-expense':
        add_expense(name=args.name, amount=args.amount, category=args.category, description=args.description)
    elif args.command == 'view-expenses':
        view_expenses(args.number, args.category)
    elif args.command == 'edit-expense':
        edit_expense()
    elif args.command == 'delete-expense':
        delete_expense(id=args.id, name=args.name, amount=args.amount, time_of_transaction=args.time, category=args.category, description=args.description)


if __name__ == '__main__':
    main()

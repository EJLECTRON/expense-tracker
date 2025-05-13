import argparse
from expense_tracker.services.category_service import add_category, view_categories, edit_category, delete_category
from expense_tracker.services.expense_service import add_expense, view_expenses, edit_expense, delete_expense

def main():
    parser = argparse.ArgumentParser(description='Expense Tracker CLI')
    subparsers = parser.add_subparsers(dest='command')


    help_main = subparsers.add_parser('--help')

    view_categories_parser = subparsers.add_parser('view-categories')

    add_category_parser = subparsers.add_parser('add-category')
    add_category_parser.add_argument('--name', type=str, required=True, help='Category name')

    edit_category_parser = subparsers.add_parser('edit-category')
    edit_category_parser.add_argument('--initial_name', type=str, required=True, help='Categoty name you want to rename')
    edit_category_parser.add_argument('--needed_name', type=str, required=True, help='Desired new name of category')

    delete_category_parser = subparsers.add_parser('delete-category')
    delete_category_parser.add_argument('--name', type=str, required=True, help='Name of the category to delete')

    add_expense_parser = subparsers.add_parser('add-expense')
    add_expense_parser.add_argument('--name', type=str, required=True, help='Header of expence')
    add_expense_parser.add_argument('--amount', type=float, required=False, help='Expense amount')
    add_expense_parser.add_argument('--category', type=str, required=False, help='Category name')
    add_expense_parser.add_argument('--description', type=str, required=False, help='Full description')

    view_expenses_parser = subparsers.add_parser('view-expenses')
    view_expenses_parser.add_argument('--amount', type=int, required=False, help='View last n expenses')
    view_expenses_parser.add_argument('--category', type=str, required=False, help='To discover all available categories use command: \n view categories')


    edit_expense_parser = subparsers.add_parser('edit-expense')
    edit_expense_parser.add_argument("--title", type=str, required=True, help="Title that represents record to edit")
    edit_expense_parser.add_argument("--new_title", type=str, required=False, help="New title for the record")
    edit_expense_parser.add_argument("--amount", type=float, required=False, help="New amount of the record")
    edit_expense_parser.add_argument("--category", type=float, required=False, help="New category of the record")
    edit_expense_parser.add_argument("--description", type=float, required=False, help="New description of the record")

    delete_expense_parser = subparsers.add_parser('delete-expense')
    delete_expense_parser.add_argument("--title", type=str, required=True, help="Title of the record to be deleted")

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
        view_expenses(amount=args.amount, category=args.category)
    elif args.command == 'edit-expense':
        edit_expense(title=args.title, new_title=args.new_title, amount=args.amount, category=args.category, description=args.description)
    elif args.command == 'delete-expense':
        delete_expense(title=args.title)


if __name__ == '__main__':
    main()

import argparse
from services.categoty_service import add_category, view_categories
from services.expense_service import add_expense, view_expenses

def main():
    parser = argparse.ArgumentParser(description='Expense Tracker CLI')
    subparsers = parser.add_subparsers(dest='command')

    add_category_parser = subparsers.add_parser('add-category')
    add_category_parser.add_argument('name', type=str, help='Categoty name')
    
    view_categories_parser = subparsers.add_parser('view-categories')
    
    add_expense_parser = subparsers.add_parser('add-expense')
    add_expense_parser.add_argument('name', type=str, help='Header of expence')
    add_expense_parser.add_argument('amount', type=float, help='Expense amount')
    add_expense_parser.add_argument('category', type=str, help='Category name')
    add_expense_parser.add_argument('description', type=str, help='Full description')
    
    view_expenses_parser = subparsers.add_parser('view-expenses')
    view_expenses_parser.add_argument('number', type=int, help='View last n expenses')
    view_expenses_parser.add_argument('category', type=str, help='To discover all available categories use command: \n view categories')
    
    args = parser.parse_args()

    if args.command == 'add-category':
        add_category(args.name)
    elif args.command == 'view-categories':
        view_categories()
    elif args.command == 'add-expense':
        add_expense(args.name, args.amount, args.category, args.description)
    elif args.command == 'view-expenses':
        view_expenses(args.number, args.category)
        

if __name__ == '__main__':
    main()

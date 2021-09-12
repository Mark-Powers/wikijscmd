from datetime import datetime, timedelta

from main import get_tree, get_single_page, create

def args_for_date(date):
    return {
        "path": date.strftime("journal/%Y/%b/%d").lower(),
        "title": date.strftime("%B %-d"),
    }


def fill_in_pages(args):
    last_date = None
    for page in get_tree(["journal"]):
        try:
            date = datetime.strptime(page["path"], "journal/%Y/%b/%d")
            if last_date is None or date > last_date:
                last_date = date
        except ValueError:
            continue
    today = datetime.now().date()
    if last_date is None:
        last_date = today
    pending_date = last_date.date()
    while pending_date < today:
        pending_date += timedelta(days=1)
        create(args_for_date(pending_date))


def today(args):
    """
    Creates a journal page with the path "journal/YYYY/MM/DD"

    args: used
    """
    args = args_for_date(datetime.now().date())
    if get_single_page(args["path"]) is not None:
        edit(args)
    else:
        create(args)

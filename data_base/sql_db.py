import sqlite3 as sq

base = sq.connect("users and tax ID.db")
cur = base.cursor()


def sql_start():
    if base:
        print("Database connected!")
    base.execute(
        '''CREATE TABLE IF NOT EXISTS TaxData(ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT, 
        Surname TEXT, 
        Email TEXT, 
        PhoneNumber TEXT, 
        TelegramID TEXT, 
        PaymentType TEXT, 
        TaxID TEXT, 
        Address TEXT, 
        RSusername TEXT, 
        RSpassword TEXT, 
        BusinessActivity TEXT, 
        EndDateTimeRegistartion TEXT, 
        MonthTransaction TEXT,
        DateTransaction TEXT,
        AllTransaction TEXT)''')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS Moderators(Name TEXT, TelegramID TEXT)')
    base.commit()


async def sql_add_command_tax(state):
    async with state.proxy() as data:
        cur.execute(
            'INSERT INTO TaxData (Name, Surname, Email, PhoneNumber, TelegramID, PaymentType, TaxID, Address, RSusername, RSpassword, BusinessActivity, EndDateTimeRegistartion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_add_payment(tg_id, state):
    async with state.proxy() as data:
        list1 = dict(zip(["MonthTransaction", "DateTransaction"], list(data.values())))
        for key, value in list1.items():
            all = cur.execute('SELECT {} FROM TaxData WHERE TelegramID == ?'.format(key), (tg_id,)).fetchall()
            if all == [(None,)]:
                cur.execute('UPDATE TaxData SET {} == ? WHERE TelegramID == ?'.format(key), (value, tg_id))
                base.commit()
            else:
                all = [i[0] for i in all]
                cur.execute('UPDATE TaxData SET {} == ? WHERE TelegramID == ?'.format(key), (", ".join([*all, value]), tg_id))
                base.commit()
        all = cur.execute('SELECT AllTransaction FROM TaxData WHERE TelegramID == ?'.format(key), (tg_id,)).fetchall()
        if all == [(None,)]:
            cur.execute('UPDATE TaxData SET AllTransaction == ? WHERE TelegramID == ?'.format(key), (" - ".join(list(data.values())), tg_id))
            base.commit()
        else:
            all = [i[0] for i in all]
            cur.execute('UPDATE TaxData SET AllTransaction == ? WHERE TelegramID == ?'.format(key), (", ".join([*all, " - ".join(list(data.values()))]), tg_id))
            base.commit()


def sql_delete_payment(tg_id):
    for i in ["MonthTransaction", "DateTransaction"]:
        cur.execute("UPDATE TaxData SET {} == NULL WHERE TelegramID == ?".format(i), (tg_id, ))
        base.commit()

def all_transaction(TelegramID):
    users = cur.execute('SELECT MonthTransaction, DateTransaction FROM TaxData WHERE TelegramID == ?', (TelegramID, )).fetchall()
    if users != [(None, )]:
        list0 = [list(zip(i[0].split(", "), i[1].split(", "))) for i in users]
        return list0


def all_telegram_id():
    users = cur.execute('SELECT Name, TelegramID FROM TaxData').fetchall()
    return users


def telegram_id():
    user = cur.execute('SELECT TelegramID FROM TaxData').fetchall()
    return user

def serial_number(TelegramID):
    number = cur.execute('SELECT ID FROM TaxData WHERE TelegramID == ?', (TelegramID, )).fetchall()
    return [i[0] for i in number]


def tg_id_declaration(ID):
    id = cur.execute('SELECT TelegramID FROM TaxData WHERE ID == ?', (ID, )).fetchall()
    return [i[0] for i in id]


def tax_data():
    users = cur.execute(
        'SELECT ID, Name, Surname, Email, PhoneNumber, PaymentType, TaxID, Address, RSusername, RSpassword, BusinessActivity, MonthTransaction, DateTransaction, AllTransaction FROM TaxData').fetchall()
    return [list(i) for i in users]

def load_tax_data(tg_id):
    users = cur.execute('SELECT ID, Name, Surname, Email, PhoneNumber, PaymentType, RSusername, RSpassword, TaxID, Address, BusinessActivity FROM TaxData WHERE TelegramID == ?', (tg_id, )).fetchone()
    return list(users)

def admin_id():
    users = cur.execute("SELECT TelegramID FROM Moderators").fetchall()
    list0 = [i[0] for i in users]
    return list0


def admin_all():
    users = cur.execute("SELECT * FROM Moderators").fetchall()
    return users


async def add_admin_id(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO Moderators (Name, TelegramID) VALUES (?, ?)", tuple(data.values()))
        base.commit()

async def sql_delete_command(data):
    cur.execute("DELETE FROM Moderators WHERE Name == ?", (data,))
    base.commit()



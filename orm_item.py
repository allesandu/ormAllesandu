import psycopg2
import psycopg2.extras
import psycopg2.extensions

credential = {
    'database':'shop',
    'user':'shop',
    'password':'shop',
    'host':'127.0.0.1',
    'port':'5432'
}

connection = None
def get_connection():
    
    global connection
    if not connection:
        connection = psycopg2.connect(**credential)
        connection.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
        )
    return connection

class Item:
    
    conn = get_connection()
    
    def __init__(self, _id=None):
        self._id = None
        self._category_id = None
        self._title = None
        self._price = None
        self._ismodified = False
        
        if _id:
            self.__load(_id);
    
    # def check(self):
    #     return self._ismodified
        
    # def mod(self):
    #     if self._ismodified == False:
    #         self._ismodified = True
    #         print("Ok")
    
    @property
    def id(self):
        return self._id
    
    @property
    def title(self):
        return self._title
    
    @property
    def price(self):
        return self._price
    
    @property
    def category_id(self):
        return self._category_id
    
    @id.setter
    def id(self, value):
        self._ismodified = True # doesnt work WHY!
        # self.mod()
        self._id = value
    
    @title.setter
    def title(self, newtitle):
        self._ismodified = True # doesnt work WHY!
        # self.mod()
        self._title = newtitle
        print("--changed Status")
    
    @price.setter
    def price(self, value):
        self._ismodified = True # doesnt work WHY!
        # self.mod()
        self._price = value
        print("--changed Status")
    
    def __load(self, _newid):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cursor.execute('SELECT * FROM "item" WHERE id = {}'.format(_newid))
        record = cursor.fetchone()
        cursor.close()
        
        for key, value in record.items():
            # setattr(self, f'_{key}', value) # WHY!!! doesnt work !!!
            setattr(self, '_{}'.format(key), value)
            # print('_{}'.format(key), value)
    
    def save(self):
        # if not self._ismodified:
        #     return
        
        self.__save()
    
    def __save(self):
    
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        if self.id: # only PRICE changing
            cursor.execute("""
                UPDATE "item"
                SET
                price = %s
                WHERE id = %s;
                """,
                (self.price, self.id)
            )
        else:
            cursor.execute("""
                INSERT INTO "item" (title, category_id, price)
                VALUES (%s, %s, %s) RETURNING id;
                """,
                (self.title, self.category_id, self.price)
            )
            self._id = cursor.fetchone()['id']
            
        cursor.close()
    

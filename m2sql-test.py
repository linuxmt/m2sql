import m2sql

m2sql.connect('veritabani.m2sql')

m2sql.execute('CREATE TABLE test (ID id, isim Text, yasi Int)')

m2sql.execute('INSERT INTO test (isim, yasi) NOT (isim)', 'deneme', 0)
m2sql.update()

for veritabani in m2sql.execute('SELECT * FROM test'):
    ID, isim, yasi = veritabani[0], veritabani[1], veritabani[2]
    print ID

m2sql.DELETE_(m2sql.table, ID)
m2sql.DELETE_('test', ID) #test -> tablo

m2sql.UPDATE_(ID, m2sql.table, 'yasi', 1)

#m2sql.table --> işlem yapılacak aktif tablo
#ID --> değişiklik yapılacak kayıt, yasi -> tablodaki sutun, 1 (int) --> yeni değer 

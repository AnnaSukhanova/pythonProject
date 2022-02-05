import sqlite3

genre = input().strip()
con = sqlite3.connect('Chinook_Sqlite.sqlite')
res = con.cursor().execute(f"""SELECT
    Track.Name as TrackName,
    Genre.Name as GenreName,
    Album.Title as AlbumTitle,
    Artist.Name
FROM
    Track
LEFT JOIN Genre ON Track.GenreId = Genre.GenreId
LEFT JOIN Album ON Track.AlbumId = Album.AlbumId
LEFT JOIN Artist ON Album.ArtistId = Artist.ArtistId
WHERE GenreName = '{genre}'
ORDER BY Artist.Name""").fetchall()
lst = []
for i in res:
    if i[-1] not in lst:
        print(i[-1])
        lst.append(i[-1])
con.close()
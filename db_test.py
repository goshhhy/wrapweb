from wrapdb import db, Project, Wrap

zlib_proj = Project("zlib")
zlib_wrap = Wrap("1.2.8", 1, "project('zlib')", b"test")
zlib_proj.wraps.append(zlib_wrap)
db.session.add(zlib_proj)
db.session.add(zlib_wrap)

db.session.commit()

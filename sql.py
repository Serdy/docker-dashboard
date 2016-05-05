from flask import g


def hosts():
	try:
		hosts = g.db.execute("SELECT * FROM hosts;").fetchall()
	except Exception:
		hosts = g.db.execute("CREATE TABLE hosts ( host_id INTEGER PRIMARY KEY AUTOINCREMENT, host_ip VARCHAR NOT NULL, domain_name, datacenter);").fetchall()

	return hosts
    
def add_host(host_ip , domain_name, datacenter):
	g.db.execute("INSERT INTO hosts (host_ip, domain_name, datacenter) VALUES (?, ?, ?)", (host_ip, domain_name, datacenter)).fetchall()
	g.db.commit()

def del_host(host_id):
	g.db.execute("DELETE FROM hosts WHERE host_id=?", (host_id,)).fetchall()
	g.db.commit()

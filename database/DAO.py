from database.DB_connect import DBConnect
from model.driver import Driver


class DAO():


    @staticmethod
    def getAllAnni():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)

        query = "SELECT distinct year FROM seasons s ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getPiloti(inizio, fine):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)

        query = """SELECT d.driverId, d.driverRef, d.number, d.code, d.forename, d.surname, d.dob, d.nationality 
FROM drivers d, races ra, results re 
where d.driverId = re.driverId and 
re.raceId = ra.raceId 
and ra.`year` between %s and %s and 
re.`position` is not null 
GROUP BY d.driverId """

        cursor.execute(query, (inizio, fine))

        for row in cursor:
            results.append(Driver(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges(inizio, fine, idMap):
        conn = DBConnect.get_connection()
        results = {}
        cursor = conn.cursor(dictionary=True)

        query = """SELECT t1.driverId d1, t2.driverId d2, count(*) tot 
FROM (select d.driverId, ra.raceId, re.constructorId 
FROM drivers d, races ra, results re 
WHERE d.driverId = re.driverId and 
re.raceId = ra.raceId and 
ra.`year` between %s and %s and 
re.`position` is not null) t1, 
(SELECT d.driverId, ra.raceId, re.constructorId 
FROM drivers d, races ra, results re 
WHERE d.driverId = re.driverId and 
re.raceId = ra.raceId and 
ra.`year` between %s and %s and 
re.`position` is not null) t2 
WHERE t1.raceId = t2.raceId and t1.constructorId =t2.constructorId and t1.driverId < t2.driverId 
GROUP BY t1.driverId, t2.driverId"""

        cursor.execute(query, (inizio, fine, inizio, fine))

        for row in cursor:
            results[(idMap[row["d1"]], idMap[row["d2"]])] = row["tot"]

        cursor.close()
        conn.close()
        return results



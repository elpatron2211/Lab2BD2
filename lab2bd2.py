from neo4j import GraphDatabase

URI="neo4j+s://f955a66e.databases.neo4j.io"
AUTH=("neo4j","9h4UWCWtkxjqM90NQrXDmDmF8O342uMJrrpRsyP58mU")
AURA_INSTANCEID="f955a66e"
AURA_INSTANCENAME="Instance01"

with GraphDatabase.driver(URI,auth=AUTH) as driver:
    driver.verify_connectivity()
MANETUQL_PAT="e0f671e2-924b-43cf-8da7-d06433d370fe"
TRACE="--trace-ascii tracefile"
FLAGS="--show-error --fail"
URL="https://portal.eu.manetu.io/graphql"
PROVIDER="pr1"
PROVIDER2="pr2"
USER="user1"
USER2="user2"

function mutate {
	QUERY=`echo '{ "query":"mutation {' $1 '}" }'`
	echo "Mutate: |$QUERY|"
	echo -n "Response: "
	curl --data "$QUERY" $TRACE $FLAGS --header 'Content-Type: application/json' -u ":$MANETUQL_PAT" "$URL"
	echo; echo
}

function query {
	QUERY=`echo '{ "query":"query {' $1 '}" }'`
	echo "Query: |$QUERY|"
	echo -n "Response: "
	curl --data "$QUERY" $TRACE $FLAGS --header 'Content-Type: application/json' -u ":$MANETUQL_PAT" "$URL"
	echo; echo
}

# Mutations

mutate 'create_vault (label:\"'$USER'\", role: USER) { label bid sid created last_updated role state }'

mutate 'upsert_vault (label:\"'$USER'\", role: USER) { label bid sid created last_updated role state }'

#Queries

#Attributes
query 'get_provider_vaults(labels:[\"'$PROVIDER'\"]) { label name attributes(sparql_expr:\"SELECT ?s ?p ?o WHERE { ?s ?p ?o }\"){ name value } }'

query 'get_password_reset_questions { last_updated questions secrets }'

query 'get_profile { name email }'

query 'get_provider { activity { last_ts } }'

query 'get_provider_policy { policy { created default_choice description from last_updated legalese to } pupid }'

query 'get_provider_task_counts { all }'

query 'get_provider_tasks { assignee description }'

query 'get_provider_vaults(labels:[\"'$USER'\"]) { name label }'

#All Vaults
query 'get_provider_vaults(scope:ALL) { label }'

query 'get_user_vaults(providers:\"'$PROVIDER'\" roles:\"ADMIN\") { label }'


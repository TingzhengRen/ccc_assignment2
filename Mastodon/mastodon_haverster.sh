### Xinyi Rui - 1135819 - xrrui@student.unimelb.edu.au
### Wenxin Zhu - 1136510 - wenxin2@student.unimelb.edu.au
### Tingzheng Ren - 1287032 - tingzhengr@student.unimelb.edu.au
### Shiqi Liang - 1420147 - liasl1@student.unimelb.edu.au
### Jingchen Shi - 1135824 - jingchens1@student.unimelb.edu.au


# Set parameters
. ./secrets.sh

### There are two servers: au & world
## au server
export URL='https://mastodon.au/api/v1'

# Test access 
curl --header "Authorization: Bearer ${MASTODON_ACCESS_TOKEN_au=}" \
     -XGET \
     -vvv \
  	 "${URL}/accounts/verify_credentials"

## world server
export URL='https://mastodon.world/api/v1'

# Test access 
curl --header "Authorization: Bearer ${MASTODON_ACCESS_TOKEN_world=}" \
     -XGET \
     -vvv \
  	 "${URL}/accounts/verify_credentials"

## user, federated (more data) and local (corresponding different URL)
curl --header "Authorization: Bearer ${MASTODON_ACCESS_TOKEN_au=}" \
     -XGET \
     -vvv \
     "${URL}/streaming/user"
	 #"${URL}/streaming/public"
	 #"${URL}/streaming/public/local"
	 
curl --header "Authorization: Bearer ${MASTODON_ACCESS_TOKEN_world=}" \
     -XGET \
     -vvv \
     "${URL}/streaming/user"
	 #"${URL}/streaming/public"
	 #"${URL}/streaming/public/local"


## user, federated and local for given hashtag (text search is not supported)
curl --header "Authorization: Bearer ${MASTODON_ACCESS_TOKEN_au=}" \
     -XGET \
     -vvv \
     "${URL}/streaming/hashtag?tag=dogecoin"
	 #"${URL}/streaming/public"
	 #"${URL}/streaming/public/local"


# full-text search (accounts, statuses, hashtag)
# Search
curl --header "Authorization: Bearer ${MASTODON_ACCESS_TOKEN=}" \
  -XGET \
  -vvv \
  -G \
  --data-urlencode "q=cats" \
  "https://mastodon.au/api/v2/search"
  #"https://mastodon.world/api/v2/search"




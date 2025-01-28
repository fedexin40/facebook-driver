query = """
    query MyQuery($first: Int!) {
      products(channel: "proyecto705", first: $first) {
        edges {
          node {
            collections {
              slug
            }
            category {
              slug
            }
            slug
            name
            description
            isAvailable
            pricing {
              priceRange {
                stop {
                  net {
                    amount
                    currency
                  }
                }
              }
            }
            media {
              url
            }
          }
          cursor
        }
      }
    }
"""

query_offset = """
    query MyQuery($first: Int!, $cursor: String!) {
      products(channel: "proyecto705", first: $first, after: $cursor) {
        edges {
          node {
            id
            name
            description
            isAvailable
            pricing {
              priceRange {
                stop {
                  net {
                    amount
                    currency
                  }
                }
              }
            }
            media {
              url
            }
          }
          cursor
        }
      }
    }
"""
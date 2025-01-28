import csv
import json
from python_graphql_client import GraphqlClient
from queries import query_offset, query
from urllib.parse import urlparse


# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="https://api.proyecto705.com/graphql/")

first = 100
variables = {"first": first}
# Synchronous request
result = client.execute(query=query, variables=variables)

link_template_string = "https://proyecto705.com/{collection}/{product_slug}"
# Write header
with open('facebook_catalog.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = [
        'id', 'title', 'description', 'availability', 'condition',
        'price', 'link', 'image_link', 'brand']
    writer.writerow(field)
    while True:
        # Get products from data
        products = result['data']['products']['edges']
        if not products:
            break
        # Get cursor from last product fetched
        cursor = products[-1]['cursor']
        variables = {"first": first, "cursor": cursor}
        for product in products:
            product = product['node']
            collection = product['collections'][0]['slug']
            id = product['slug']
            title = product['name']
            description = product['description']
            description = str(
                json.loads(description)['blocks'][1]['data']['text'] if description
                else ''
            )
            description = description.replace('&nbsp;', '')
            availability = 'in stock' if product['isAvailable'] else 'out of stock'
            # I only sell new products :)
            condition = 'new'
            price = ' '.join([
                str(product['pricing']['priceRange']['stop']['net']['amount']),
                str(product['pricing']['priceRange']['stop']['net']['currency'])
            ])
            # It is possible to have more than one image, then I am taking the
            # first one
            image_link = product['media'][0]['url']
            url = "https://proyecto705.com/Colecciones/{collection}/{product_slug}".format(
                collection=collection, product_slug=product['slug']
            )
            brand = 'Proyecto 705'
            writer.writerow(
                [id, title, description, availability, condition,
                 price, url, image_link, brand])
        # Lets get the next products
        variables = {"first": first, "cursor": cursor}
        result = client.execute(query=query_offset, variables=variables)

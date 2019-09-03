#!/usr/bin/env xonsh

curl https://developer.github.com/v4/public_schema/schema.public.graphql -o gqlmod_github/schema.graphql

# TODO: Generate scalar/serialization data

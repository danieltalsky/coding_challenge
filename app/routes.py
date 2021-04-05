import logging

import flask
from flask import jsonify, Response

from app.adapters import get_org_data_for_github, get_org_data_for_bitbucket
from app.network import Api, RateLimitExceeded, ResourceNotFound, UnknownNetworkError
from app.organization import InvalidOrganizationName, Organization

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)


# MAJOR @TODO: ADD DOCKER CONTAINER STARTUP
# MAJOR @TODO: ADD TEST HARNESS
@app.route("/organization/<string:organization_name>", methods=["GET"])
def organization(organization_name: str):
    """
    Get and merge organization details for multiple git hosts
    """
    try:
        org = Organization(organization_name)
        app.logger.info(f"valid org name found: {org.name}")
        api = Api()
        org = get_org_data_for_github(org, api, version=4)
        org = get_org_data_for_bitbucket(org, api, version=2)
    except InvalidOrganizationName as ion:
        app.logger.error(f"Invalid organization name: {organization_name}")
        return Response("Invalid organization name.", status=400)
    except ResourceNotFound as rnf:
        app.logger.error(f"Organization does not exist:  {organization_name}")
        return Response("Organization does not exist.", status=400)
    except RateLimitExceeded as rle:
        app.logger.error(f"Rate limit. URL: {str(rle)}")
        return Response("Please try again later.", status=400)
    except UnknownNetworkError as une:
        app.logger.error(f"Unknown network error. URL: {str(une)}")
        return Response("Unknown network error.", status=400)
    # except Exception as e:
    #     app.logger.error(f"Exception: {str(e)}")
    #     return Response("Something went wrong!", status=400)

    return jsonify(org.json_data), 200

#!/usr/bin/env bash

export ATD_IMAGE="atddocker/atd-cris-capybara";

#
# By default we are going to assume the current branch will be deployed to the dev server
#
export ATD_AWS_LAMBDA_ENV="dev";

#
# If this is production or staging, assign the variable accordingly.
#
if [[ "${CIRCLE_BRANCH}" == "production" ]]; then
    export ATD_AWS_LAMBDA_ENV="production";
elif [[ "${CIRCLE_BRANCH}" == "master" ]]; then
    export ATD_AWS_LAMBDA_ENV="master";
fi;

function deploy_aws_lambda {
    echo "Updating AWS Lambda"
    zappa update $ATD_AWS_LAMBDA_ENV;
}
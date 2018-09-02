#!/bin/bash
# used for creating deployment package of lambda

package_name="lambda.zip"

#------------------------------------------------
shopt -s extglob
rm -f ${package_name}
zip ${package_name} -r !(docs)
#!/bin/bash
# used for creating deployment package of lambda

package_name="lambda.zip"

#------------------------------------------------

rm -f ${lambda.zip}
zip ${lambda.zip} -r .
# Open Source Medical Imaging Tools on AWS

This repository contains the templates and resources for launching the open source [DICOM](https://www.dicomstandard.org/) medical image servers [DCM4CHEE](https://github.com/dcm4che/dcm4chee-arc-light/wiki) and [Orthanc](https://www.orthanc-server.com/) on the AWS cloud. These solutions each provide a DICOM service accessible through either [DICOM DIMSE](http://dicom.nema.org/dicom/2013/output/chtml/part07/sect_7.5.html) or [DICOMWeb](https://www.dicomstandard.org/dicomweb) protocols, accessible via the Internet.

## Description

Each of these two solutions is deployed by means of an [AWS CloudFormation](https://aws.amazon.com/cloudformation) template.  On launching the template in the AWS Console, the user is presented with a number of configuration options relevant to the DICOM server application (DCM4CHEE or Orthanc) and its supporting infrastructure (networking, storage, database, security, etc). Deployment from this point is automatic, and results in a fully running solution providing DICOM services at an internet-accessible endpoint.

Both solutions run the DICOM server application in a Docker container on [Amazon Elastic Container Service](https://aws.amazon.com/ecs) (ECS).  Image files are stored on [Amazon Elastic File System](https://aws.amazon.com/efs/) (EFS), and indexes are stored in PostgreSQL running on [Amazon Relational Database Service](https://aws.amazon.com/rds/) (RDS).

For more information, see the descriptions for [DCM4CHEE on AWS](https://github.com/aws-samples/open-source-medical-imaging-tools-on-aws/tree/main/dcm4chee) and [Orthanc on AWS](https://github.com/aws-samples/open-source-medical-imaging-tools-on-aws/tree/main/orthanc).

## Installation

Each solution is launched from CloudFormation.  Either clone this repository and upload the template file for the solution to CloudFormation, or use the one-click deployment link in the README file of the solution.

## Prerequisites

To deploy each of these solutions you will require:
* An AWS account, with console access and the rights to launch AWS resources.
* An existing [Virtual Private Cloud](https://aws.amazon.com/vpc) (VPC) within your account.  A suitable VPC can be created by deploying the AWS [Modular and Scalable VPC Architecture](https://aws.amazon.com/quickstart/architecture/vpc/) QuickStart.

## Authors

These solutions were developed by AWS Solutions Architects and are provided as [AWS Samples](https://github.com/aws-samples/).

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.


## License

This project is licensed under the [MIT-0](https://github.com/aws/mit-0) License - see the [LICENSE](LICENSE) file for details

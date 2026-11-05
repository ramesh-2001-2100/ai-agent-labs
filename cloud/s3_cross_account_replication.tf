terraform {
  required_version = ">= 1.3.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region in which to create the replication lab resources."
  type        = string
  default     = "us-east-1"
}

variable "source_bucket_name" {
  description = "Name of the source S3 bucket."
  type        = string
  default     = "my-source-bucket-unique"
}

variable "destination_bucket_name" {
  description = "Name of the destination S3 bucket."
  type        = string
  default     = "my-destination-bucket-unique"
}

variable "replication_role_name" {
  description = "Name of the IAM role used by S3 replication."
  type        = string
  default     = "s3-replication-role"
}

variable "replication_policy_name" {
  description = "Name of the IAM policy attached to the replication role."
  type        = string
  default     = "s3-replication-policy"
}

variable "replication_rule_id" {
  description = "Identifier for the S3 replication rule."
  type        = string
  default     = "prefix-tag-replication"
}

variable "replication_prefix" {
  description = "Object key prefix selected by the replication rule."
  type        = string
  default     = "logs/"
}

variable "replication_tag_key" {
  description = "Object tag key used to select objects for replication."
  type        = string
  default     = "env"
}

variable "replication_tag_value" {
  description = "Object tag value used to select objects for replication."
  type        = string
  default     = "prod"
}

# The two buckets intentionally use the default provider and therefore remain
# in the same AWS account. Their names retain the values used by this lab.
resource "aws_s3_bucket" "source" {
  bucket = var.source_bucket_name
}

resource "aws_s3_bucket" "destination" {
  bucket = var.destination_bucket_name
}

resource "aws_s3_bucket_versioning" "source" {
  bucket = aws_s3_bucket.source.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "destination" {
  bucket = aws_s3_bucket.destination.id

  versioning_configuration {
    status = "Enabled"
  }
}

data "aws_iam_policy_document" "replication_assume_role" {
  statement {
    sid    = "AllowS3ToAssumeReplicationRole"
    effect = "Allow"

    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["s3.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "replication" {
  statement {
    sid    = "ReadSourceBucketConfiguration"
    effect = "Allow"

    actions = [
      "s3:GetReplicationConfiguration",
      "s3:ListBucket",
    ]

    resources = [aws_s3_bucket.source.arn]
  }

  statement {
    sid    = "ReadSourceObjectVersions"
    effect = "Allow"

    actions = [
      "s3:GetObjectVersionForReplication",
      "s3:GetObjectVersionAcl",
      "s3:GetObjectVersionTagging",
    ]

    resources = ["${aws_s3_bucket.source.arn}/*"]
  }

  statement {
    sid    = "WriteReplicatedObjects"
    effect = "Allow"

    actions = [
      "s3:ReplicateObject",
      "s3:ReplicateDelete",
      "s3:ReplicateTags",
    ]

    resources = ["${aws_s3_bucket.destination.arn}/*"]
  }
}

resource "aws_iam_role" "replication" {
  name        = var.replication_role_name
  description = "Role assumed by S3 to replicate objects between the lab buckets."

  assume_role_policy = data.aws_iam_policy_document.replication_assume_role.json
}

resource "aws_iam_policy" "replication" {
  name        = var.replication_policy_name
  description = "Least-privilege permissions for S3 bucket replication."
  policy      = data.aws_iam_policy_document.replication.json
}

resource "aws_iam_role_policy_attachment" "replication" {
  role       = aws_iam_role.replication.name
  policy_arn = aws_iam_policy.replication.arn
}

resource "aws_s3_bucket_replication_configuration" "source" {
  bucket = aws_s3_bucket.source.id
  role   = aws_iam_role.replication.arn

  # S3 requires versioning and the role policy before a replication rule can
  # be created, even though those resources are not all referenced by arguments.
  depends_on = [
    aws_s3_bucket_versioning.source,
    aws_s3_bucket_versioning.destination,
    aws_iam_role_policy_attachment.replication,
  ]

  rule {
    id     = var.replication_rule_id
    status = "Enabled"

    filter {
      and {
        prefix = var.replication_prefix

        tags = {
          (var.replication_tag_key) = var.replication_tag_value
        }
      }
    }

    destination {
      bucket        = aws_s3_bucket.destination.arn
      storage_class = "STANDARD"
    }

    delete_marker_replication {
      status = "Enabled"
    }
  }
}

output "source_bucket_arn" {
  description = "ARN of the source S3 bucket."
  value       = aws_s3_bucket.source.arn
}

output "destination_bucket_arn" {
  description = "ARN of the destination S3 bucket."
  value       = aws_s3_bucket.destination.arn
}

output "replication_role_arn" {
  description = "ARN of the IAM role used by S3 replication."
  value       = aws_iam_role.replication.arn
}

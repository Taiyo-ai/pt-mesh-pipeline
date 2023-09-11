terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.7.0"
    }
  }
}

provider "aws" {
  region = "eu-west-3"
}

module "ecr" {
  source = "github.com/byu-oit/terraform-aws-ecr?ref=v1.0.1"
  name   = "tenders_epi_hvt_central/ingestion"
}

module "lambda_image" {
  source             = "../../../utils/tfmodules/terraform-aws-ecr-image"
  dockerfile_dir     = "../../src"
  ecr_repository_url = module.ecr.repository.repository_url
  docker_image_tag   = "%TAG%"
  depends_on         = [module.ecr]
}

data "aws_eks_cluster" "projects" {
  name = "projects"
}

data "aws_eks_cluster_auth" "projects" {
  name = "projects"
}


provider "kubectl" {
  host                   = data.aws_eks_cluster.projects.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.projects.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.projects.token
  load_config_file       = false
}

data "kubectl_filename_list" "manifests" {
  pattern = "./*.yaml"
}

resource "kubectl_manifest" "serving" {
  count      = length(data.kubectl_filename_list.manifests.matches)
  yaml_body  = file(element(data.kubectl_filename_list.manifests.matches, count.index))
  depends_on = [module.lambda_image]
}

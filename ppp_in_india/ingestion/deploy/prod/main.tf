module "taiyo_harvester" {
    source               = "../../../../utils/tfmodules/taiyo-harvester"
    role_name            = "lambda_tutorial_role"
    policy_name          = "lambda_tutorial_policy"
    service_role         = file("iam/service-role.json")
    service_policy       = file("iam/service-policies.json")
    function_name        = "lambda_tutorial_list_buckets"
    function_description = "Lists Buckets on aws based on invocation"
    image                = ""
    version_tag          = "latest"
    # controlling the schedule of the lambda function
    target_id            = "lambda_tutorial_event" 
    trigger_name         = "lambda_tutorial_trigger"
    trigger_description  = "Trigger lambda_tutorial_list_buckets every 2 mins"
    trigger_schedule     = "cron(30 19 ? * * *)" # utc 
    input_template       = "./test.json"
}
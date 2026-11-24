import ast
from datetime import datetime
import logging

logger = logging.getLogger("etl")

def transform_record(item):
 

    user_id = item["lti_user_id"]
    if not isinstance(user_id, str) or not user_id.strip():
        raise ValueError("Incorrect user_id")
    
    try:
        passback_params = ast.literal_eval(item["passback_params"])
    except (ValueError, SyntaxError, TypeError) as e:
        raise ValueError(f"Cheto tam stalo xz{e}")
    if not isinstance(passback_params, dict):
        raise ValueError("Должен быть словарь")
    
    # три поля из пассбак парамс
    oauth_consumer_key = passback_params.get("oauth_consumer_key")
    if oauth_consumer_key is not None and not isinstance(oauth_consumer_key, str):
        raise ValueError("Incroorect pole")
    lis_result_sourcedid = passback_params.get("lis_result_sourcedid")
    if lis_result_sourcedid is not None and not isinstance(lis_result_sourcedid, str):
        raise ValueError("Incroorect pole")
    lis_outcome_service_url = passback_params.get("lis_outcome_service_url")
    if lis_outcome_service_url is not None and not isinstance(lis_outcome_service_url, str):
        raise ValueError("Incroorect pole")

    # аттемпт коррект и креатед_ат
    attempt_type = item["attempt_type"]
    if attempt_type not in ["run", "submit"]:
         raise ValueError("Something go wrong")
    
    
    is_correct = item["is_correct"]
    if attempt_type == "run" and is_correct is not None:
         raise ValueError("Для run поле корректности должно быть None")
    if attempt_type == "submit" and not isinstance(is_correct, bool):
         raise ValueError("Для сабмит поле корректности должно быть булевым")
    try:
        created_at = datetime.strptime(item["created_at"],  "%Y-%m-%d %H:%M:%S.%f")
    except (ValueError, TypeError, KeyError) as e:
         raise ValueError(f"Некорректная дата: {e}")
         
    #ретурн
    return {
        "user_id": user_id,
        "oauth_consumer_key": oauth_consumer_key,
        "lis_result_sourcedid": lis_result_sourcedid,
        "lis_outcome_service_url":lis_outcome_service_url,
        "is_correct":is_correct,
        "attempt_type":attempt_type,
        "created_at":created_at
    }

def transform_data(data):
    logger.info("Starting data transformation")   
    errors_count = 0
    transformed_data = []
    for item in data:
        try:
            obrabotan = transform_record(item)
            transformed_data.append(obrabotan)
        except (ValueError, KeyError, TypeError):
            errors_count +=1
            continue
    logger.info(
        "Data transformation completed: %s successful, %s rejected",
        len(transformed_data),
        errors_count
    )
    return transformed_data, errors_count
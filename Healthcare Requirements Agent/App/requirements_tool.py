def get_requirements_template():
    return {
        "business_request_summary": "",
        "user_story": "",
        "acceptance_criteria": [],
        "functional_requirements": [],
        "security_privacy_considerations": [],
        "test_cases": [],
        "source_references": []
    }


def get_security_requirements():
    return {
        "authentication": [],
        "authorization": [],
        "privacy": [],
        "logging": [],
        "data_protection": []
    }


def get_test_case_template():
    return {
        "positive_tests": [],
        "negative_tests": [],
        "security_tests": [],
        "edge_cases": []
    }


if __name__ == "__main__":
    print(get_requirements_template())
    print(get_security_requirements())
    print(get_test_case_template())

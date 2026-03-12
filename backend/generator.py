def enhance_prompt(user_prompt: str, domain: str) -> str:
    """
    Enhances a user prompt with domain-specific keywords for better 3D model matching.
    Currently used as a utility for future AI-based generation integration.
    """
    domain_prompts = {
        "human": "realistic human anatomy, anatomical accuracy, neutral pose, 3D model",
        "mechanical": "detailed mechanical parts, engineering design, CAD style 3D model",
        "furniture": "modern furniture design, realistic materials, 3D object",
        "architecture": "architectural structure, realistic building design, 3D model"
    }

    suffix = domain_prompts.get(domain, "")
    if suffix:
        return f"{user_prompt}, {suffix}"
    return user_prompt

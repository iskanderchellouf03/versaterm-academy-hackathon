def _lazy_home():
    from src.modules.home import render
    render()


def _lazy_company_resources():
    from src.modules.company_resources import render
    render()


def _lazy_onboarding_planner():
    from src.modules.onboarding_planner import render
    render()


def _lazy_kb_article_generator():
    from src.modules.kb_article_generator import render
    render()


def _lazy_requirement_analyzer():
    from src.modules.requirement_analyzer import render
    render()


def _lazy_qa_test_lab():
    from src.modules.qa_test_lab import render
    render()


MODULES = {
    "\U0001f3e0  Home": _lazy_home,
    "\U0001f4da  Company Resources": _lazy_company_resources,
    "\U0001f680  Onboarding Planner": _lazy_onboarding_planner,
    "\U0001f4dd  Smart Writer": _lazy_kb_article_generator,
    "\U0001f50d  Requirement Analyzer": _lazy_requirement_analyzer,
    "\U0001f9ea  QA Test Lab": _lazy_qa_test_lab,
}

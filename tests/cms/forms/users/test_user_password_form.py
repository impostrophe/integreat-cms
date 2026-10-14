from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model

from integreat_cms.cms.forms.users.user_password_form import UserPasswordForm


@pytest.mark.django_db
def test_password_form_rejects_password_similar_to_user_attributes() -> None:
    """Password validation needs the user instance for similarity checks (see #4333)."""
    user = get_user_model().objects.create_user(
        username="alicesmith",
        password="A-secure-old-password!",
    )
    form = UserPasswordForm(
        data={
            "old_password": "A-secure-old-password!",
            "new_password": "alicesmith",
            "new_password_confirm": "alicesmith",
        },
        instance=user,
    )

    assert not form.is_valid()
    assert "new_password" in form.errors

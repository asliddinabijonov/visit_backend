const initCommentFilter = () => {
  const targetObjectField = document.getElementById("id_target_object");
  const targetTypeField = document.getElementById("id_target_type");
  const objectIdField = document.getElementById("id_object_id");

  if (!targetObjectField || !targetTypeField) {
    return;
  }

  const disableSelect2 = (select) => {
    const djangoJQuery = window.django && window.django.jQuery;
    if (!djangoJQuery || !djangoJQuery.fn || !djangoJQuery.fn.select2 || !select) {
      return;
    }

    const $select = djangoJQuery(select);
    if ($select.hasClass("select2-hidden-accessible")) {
      $select.select2("destroy");
    }
    $select.removeClass("select2-hidden-accessible");
    $select.css({
      position: "",
      width: "",
      height: "",
      opacity: "",
      pointerEvents: "",
    });

    const nextContainer = select.nextElementSibling;
    if (nextContainer && nextContainer.classList.contains("select2")) {
      nextContainer.remove();
    }
  };

  const syncFields = () => {
    const rawValue = targetObjectField.value || "";
    if (!rawValue.includes(":")) {
      if (objectIdField) {
        objectIdField.value = "";
      }
      return;
    }

    const [targetType, objectId] = rawValue.split(":", 2);
    targetTypeField.value = targetType || "";
    if (objectIdField) {
      objectIdField.value = objectId || "";
    }
  };

  disableSelect2(targetTypeField);
  disableSelect2(targetObjectField);

  targetObjectField.addEventListener("change", syncFields);
  syncFields();
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initCommentFilter);
} else {
  initCommentFilter();
}

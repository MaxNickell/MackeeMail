function delete_message(message_id) {
  fetch("/delete-message", {
    method: "POST",
    body: JSON.stringify({ message_id: message_id }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function delete_global_message(global_message_id) {
  fetch("/delete-global-message", {
    method: "POST",
    body: JSON.stringify({ global_message_id: global_message_id }),
  }).then((_res) => {
    window.location.href = "/messageboard";
  });
}

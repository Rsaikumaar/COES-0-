let mediaRecorder;
let chunks = [];

function startRecording() {
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) {
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.start();
      chunks = [];

      mediaRecorder.addEventListener("dataavailable", function(event) {
        chunks.push(event.data);
      });
    });
}

function stopRecording() {
  mediaRecorder.stop();
}

function uploadAudio() {
  if (chunks.length === 0) {
    console.log("No recorded audio available.");
    return;
  }

  let blob = new Blob(chunks, { type: "audio/webm" });
  let formData = new FormData();
  formData.append("audio", blob, "recorded_audio.webm");

  $.ajax({
    type: "POST",
    url: "/process",
    data: formData,
    processData: false,
    contentType: false,
    success: function(response) {
      console.log("Audio uploaded successfully.");
    },
    error: function(xhr, status, error) {
      console.log("Error uploading audio:", error);
    }
  });
}

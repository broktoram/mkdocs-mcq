// Fixed version of mcq.js with corrected logic

function initializeMcqs() {
  // This setup logic for individual questions remains the same
  document.querySelectorAll(".mcq-container").forEach((mcq) => {
    const choicesList = mcq.querySelector(".mcq-choices ul.task-list");
    const mcqType = mcq.dataset.mcqType;
    if (!choicesList) return;

    choicesList.querySelectorAll("input").forEach((input) => {
      input.addEventListener("change", () => {
        const parentLabel = input.parentElement;
        if (mcqType === "single") {
          choicesList
            .querySelectorAll("label")
            .forEach((lbl) => lbl.classList.remove("is-selected"));
        }
        parentLabel.classList.toggle("is-selected", input.checked);
      });
    });

    if (mcqType === "single") {
      const name = `mcq-${Math.random().toString(36).substr(2, 9)}`;
      choicesList
        .querySelectorAll('input[type="checkbox"]')
        .forEach((checkbox) => {
          checkbox.type = "radio";
          checkbox.name = name;
        });
    }
  });

  // Centralized form submission logic
  const mcqForm = document.getElementById("mkdocs-mcq-form");

  if (mcqForm) {
    mcqForm.addEventListener("submit", (event) => {
      event.preventDefault();

      const singleSubmitButton = document.getElementById("mcq-quiz-submit");
      if (singleSubmitButton) {
        singleSubmitButton.style.display = "none";
      }

      let correctlyAnsweredQuestions = 0;
      const allMcqs = mcqForm.querySelectorAll(".mcq-container");
      const totalQuestions = allMcqs.length;

      allMcqs.forEach((mcq) => {
        mcq.classList.add("answered");
        const encodedKey = mcq.dataset.key;
        let correctIndices = [];
        try {
          correctIndices = JSON.parse(atob(encodedKey));
        } catch (e) {
          console.error("Could not parse answer key.", e);
          return;
        }

        const choicesList = mcq.querySelector(".mcq-choices ul.task-list");

        // FIX 1: Collect user's selected answers properly
        let userSelectedIndices = [];
        choicesList
          .querySelectorAll("li.task-list-item")
          .forEach((item, index) => {
            const checkbox = item.querySelector("input");
            if (checkbox && checkbox.checked) {
              userSelectedIndices.push(index);
            }
          });

        // FIX 2: Correct logic for determining if question is answered correctly
        // A question is correct if and only if the user selected exactly the correct answers
        const isQuestionCorrect =
          correctIndices.length === userSelectedIndices.length &&
          correctIndices.every((idx) => userSelectedIndices.includes(idx));

        // Apply visual styling to choices
        choicesList
          .querySelectorAll("li.task-list-item")
          .forEach((item, index) => {
            const checkbox = item.querySelector("input");
            const isChecked = checkbox ? checkbox.checked : false;
            const isCorrectOption = correctIndices.includes(index);

            if (isCorrectOption && isChecked) item.classList.add("correct");
            else if (!isCorrectOption && isChecked)
              item.classList.add("incorrect");
            else if (isCorrectOption && !isChecked)
              item.classList.add("was-correct");

            const wasMissedCorrect = item.classList.contains("was-correct");

            // FIX 3: Better feedback handling with proper validation
            const encodedFeedback = item.dataset.feedback;

            if (isChecked || wasMissedCorrect) {
              let statusLabel = "";
              if (item.classList.contains("correct"))
                statusLabel = "<span class='mcq-status-label'>(CORRECT)</span>";
              else if (item.classList.contains("incorrect"))
                statusLabel =
                  "<span class='mcq-status-label'>(INCORRECT)</span>";
              else if (wasMissedCorrect)
                statusLabel = "<span class='mcq-status-label'>(MISSED)</span>";

              // Only create the feedback div if there is a label or feedback text
              if (
                statusLabel ||
                (encodedFeedback && encodedFeedback.trim() !== "")
              ) {
                const feedbackDiv = document.createElement("div");
                feedbackDiv.classList.add("mcq-feedback");
                let finalHtml = "";

                if (encodedFeedback && encodedFeedback.trim() !== "") {
                  try {
                    // Decode the feedback from Base64
                    const feedbackHtml = atob(encodedFeedback);

                    if (feedbackHtml.trim() !== "") {
                      // Create a temporary element to safely append the suffix
                      const tempDiv = document.createElement("div");
                      tempDiv.innerHTML = feedbackHtml;
                      const firstChild = tempDiv.querySelector(":first-child");

                      if (firstChild) {
                        firstChild.innerHTML += " " + statusLabel;
                        finalHtml = tempDiv.innerHTML;
                      } else {
                        finalHtml = feedbackHtml + " " + statusLabel;
                      }
                    } else {
                      finalHtml = "<p>" + statusLabel + "</p>";
                    }
                  } catch (e) {
                    console.warn("Failed to decode feedback:", e);
                    finalHtml = "<p>" + statusLabel + "</p>";
                  }
                } else {
                  finalHtml = "<p>" + statusLabel + "</p>";
                }

                feedbackDiv.innerHTML = finalHtml;
                item
                  .querySelector("label")
                  .insertAdjacentElement("afterend", feedbackDiv);
              }
            }
          });

        if (isQuestionCorrect) {
          correctlyAnsweredQuestions++;
        }
      });

      // The results banner logic remains the same
      const resultsDiv = document.createElement("div");
      resultsDiv.className = "admonition info";
      resultsDiv.innerHTML = `
        <p class="admonition-title">Quiz Results</p>
        <p>You answered ${correctlyAnsweredQuestions} out of ${totalQuestions} questions correctly.</p>
      `;
      mcqForm.append(resultsDiv);
    });
  }
}

// Standard loader logic remains the same
if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    initializeMcqs();
  });
} else {
  document.addEventListener("DOMContentLoaded", initializeMcqs);
}

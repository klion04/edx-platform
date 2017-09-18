/* globals gettext */

export class CourseGoals {  // eslint-disable-line import/prefer-default-export

  constructor(options) {
    $('.goal-option').click((e) => {
      const goalKey = $(e.target).data().choice;
      $.ajax({
        method: 'POST',
        url: options.setGoalUrl,
        headers: { 'X-CSRFToken': $.cookie('csrftoken') },
        data: {
          goal_key: goalKey,
          course_key: options.courseId,
          user: options.username,
        },
        dataType: 'json',
        success: () => {
          // LEARNER-2522 will address the success message
          // xss-lint: disable=javascript-jquery-html
          $('.message-content').html('You have successfully set your goal');
        },
        error: () => {
          // LEARNER-2522 will address the error message
          // xss-lint: disable=javascript-jquery-html
          $('.message-content').html(
              gettext('There was an error in setting your goal, please reload the page and try again.'),
          );
        },
      });
    });

    // Allow goal selection with an enter press for accessibility purposes
    $('.goal-option').keyup((e) => {
      if (e.which === 13) {
        $(e.target).trigger('click');
      }
    });
  }
}

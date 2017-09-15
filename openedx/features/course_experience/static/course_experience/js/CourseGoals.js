/* globals gettext */

export class CourseGoals {  // eslint-disable-line import/prefer-default-export

  constructor(options) {
    $('.goal-option').click((e) => {
      const goalKey = $(e.target).data().choice;
      $.post({
        url: options.setGoalUrl,
        data: {
          goal_key: goalKey,
          course_id: options.courseId,
        },
        dataType: 'json',
        success: (data) => {
          // LEARNER-2522 will address the success message
          // xss-lint: disable=javascript-jquery-html
          $('.message-content').html(data.html);
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

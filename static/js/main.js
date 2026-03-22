/**
 * StudentPortal – main.js
 * jQuery: DOM manipulation, form validation, UI effects
 */

$(document).ready(function () {

  /* ═══════════════════════════════════════════════
     1. AUTO-DISMISS FLASH ALERTS
  ══════════════════════════════════════════════════ */
  setTimeout(function () {
    $('.alert.alert-dismissible').fadeOut(600, function () {
      $(this).remove();
    });
  }, 5000);


  /* ═══════════════════════════════════════════════
     2. PASSWORD VISIBILITY TOGGLE
  ══════════════════════════════════════════════════ */
  $(document).on('click', '.toggle-password', function () {
    const targetId = $(this).data('target');
    const $input   = $('#' + targetId);
    const $icon    = $(this).find('i');

    if ($input.attr('type') === 'password') {
      $input.attr('type', 'text');
      $icon.removeClass('bi-eye').addClass('bi-eye-slash');
    } else {
      $input.attr('type', 'password');
      $icon.removeClass('bi-eye-slash').addClass('bi-eye');
    }
  });


  /* ═══════════════════════════════════════════════
     3. REGISTRATION FORM VALIDATION
  ══════════════════════════════════════════════════ */
  function showError($field, $errorEl, msg) {
    $field.addClass('is-invalid');
    $errorEl.text(msg).removeClass('d-none');
  }

  function clearError($field, $errorEl) {
    $field.removeClass('is-invalid').addClass('is-valid');
    $errorEl.addClass('d-none');
  }

  // Password strength meter
  $('#regPassword').on('input', function () {
    const val = $(this).val();
    $('#strengthBar').removeClass('d-none');
    const $bar  = $('#strengthProgress');
    const $text = $('#strengthText');

    let score = 0;
    if (val.length >= 6)                    score++;
    if (val.length >= 10)                   score++;
    if (/[A-Z]/.test(val))                  score++;
    if (/[0-9]/.test(val))                  score++;
    if (/[^A-Za-z0-9]/.test(val))          score++;

    const levels = [
      { pct: 20,  cls: 'bg-danger',  label: 'Very Weak' },
      { pct: 40,  cls: 'bg-warning', label: 'Weak'      },
      { pct: 60,  cls: 'bg-info',    label: 'Fair'      },
      { pct: 80,  cls: 'bg-primary', label: 'Strong'    },
      { pct: 100, cls: 'bg-success', label: 'Very Strong'},
    ];
    const lvl = levels[Math.min(score, 4)];
    $bar.css('width', lvl.pct + '%').attr('class', 'progress-bar ' + lvl.cls);
    $text.text(lvl.label);
  });

  $('#registerForm').on('submit', function (e) {
    let valid = true;

    const name    = $('#name').val().trim();
    const email   = $('#regEmail').val().trim();
    const pwd     = $('#regPassword').val();
    const confirm = $('#confirmPassword').val();
    const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Name
    if (!name) {
      showError($('#name'), $('#nameError'), 'Full name is required.');
      valid = false;
    } else {
      clearError($('#name'), $('#nameError'));
    }

    // Email
    if (!email || !emailRe.test(email)) {
      showError($('#regEmail'), $('#regEmailError'), 'Enter a valid email address.');
      valid = false;
    } else {
      clearError($('#regEmail'), $('#regEmailError'));
    }

    // Password
    if (pwd.length < 6) {
      showError($('#regPassword'), $('#regPasswordError'), 'Password must be at least 6 characters.');
      valid = false;
    } else {
      clearError($('#regPassword'), $('#regPasswordError'));
    }

    // Confirm password
    if (pwd !== confirm) {
      showError($('#confirmPassword'), $('#confirmError'), 'Passwords do not match.');
      valid = false;
    } else if (confirm.length > 0) {
      clearError($('#confirmPassword'), $('#confirmError'));
    }

    if (!valid) e.preventDefault();
  });

  // Live confirm-password check
  $('#confirmPassword').on('input', function () {
    const pwd     = $('#regPassword').val();
    const confirm = $(this).val();
    if (confirm && confirm !== pwd) {
      showError($(this), $('#confirmError'), 'Passwords do not match.');
    } else if (confirm) {
      clearError($(this), $('#confirmError'));
    }
  });


  /* ═══════════════════════════════════════════════
     4. LOGIN FORM VALIDATION
  ══════════════════════════════════════════════════ */
  $('#loginForm').on('submit', function (e) {
    let valid = true;
    const email = $('#loginEmail').val().trim();
    const pwd   = $('#loginPassword').val();
    const re    = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!email || !re.test(email)) {
      showError($('#loginEmail'), $('#loginEmailError'), 'Enter a valid email address.');
      valid = false;
    } else {
      clearError($('#loginEmail'), $('#loginEmailError'));
    }

    if (!pwd) {
      showError($('#loginPassword'), $('#loginPasswordError'), 'Password is required.');
      valid = false;
    } else {
      clearError($('#loginPassword'), $('#loginPasswordError'));
    }

    if (!valid) e.preventDefault();
  });


  /* ═══════════════════════════════════════════════
     5. ADD TRANSACTION FORM VALIDATION
  ══════════════════════════════════════════════════ */
  // Swap category options when type changes
  $('input[name="type"]').on('change', function () {
    const isIncome = $(this).val() === 'income';
    const $cat     = $('#category');

    if (isIncome) {
      $cat.find('optgroup#expenseCats option').prop('disabled', true);
      $cat.find('optgroup#incomeCats  option').prop('disabled', false);
      $cat.find('optgroup#incomeCats  option:first').prop('selected', true);
    } else {
      $cat.find('optgroup#incomeCats  option').prop('disabled', true);
      $cat.find('optgroup#expenseCats option').prop('disabled', false);
      $cat.find('optgroup#expenseCats option:first').prop('selected', true);
    }
  });

  $('#transactionForm').on('submit', function (e) {
    let valid  = true;
    const cat  = $('#category').val();
    const amt  = parseFloat($('#amount').val());
    const date = $('#txnDate').val();

    if (!cat) {
      showError($('#category'), $('#categoryError'), 'Please select a category.');
      valid = false;
    } else {
      clearError($('#category'), $('#categoryError'));
    }

    if (!$('#amount').val() || isNaN(amt) || amt <= 0) {
      showError($('#amount'), $('#amountError'), 'Enter a valid positive amount.');
      valid = false;
    } else {
      clearError($('#amount'), $('#amountError'));
    }

    if (!date) {
      showError($('#txnDate'), $('#dateError'), 'Please select a date.');
      valid = false;
    } else {
      clearError($('#txnDate'), $('#dateError'));
    }

    if (!valid) e.preventDefault();
  });

  // Live amount formatting hint
  $('#amount').on('blur', function () {
    const val = parseFloat($(this).val());
    if (!isNaN(val) && val > 0) {
      $(this).val(val.toFixed(2));
    }
  });


  /* ═══════════════════════════════════════════════
     6. DELETE TRANSACTION (Confirm Modal)
  ══════════════════════════════════════════════════ */
  let $pendingDeleteForm = null;
  const deleteModal      = new bootstrap.Modal('#deleteModal');

  $(document).on('click', '.delete-btn', function () {
    $pendingDeleteForm = $(this).closest('.delete-form');
    const msg = $pendingDeleteForm.data('confirm') || 'Delete this transaction?';
    $('#deleteModalMsg').text(msg);
    deleteModal.show();
  });

  $('#confirmDeleteBtn').on('click', function () {
    if ($pendingDeleteForm) {
      $pendingDeleteForm.submit();
    }
    deleteModal.hide();
  });


  /* ═══════════════════════════════════════════════
     7. WITHDRAW APPLICATION (Confirm Modal)
  ══════════════════════════════════════════════════ */
  let $pendingWithdrawForm = null;
  const withdrawModal      = $('#withdrawModal').length
    ? new bootstrap.Modal('#withdrawModal')
    : null;

  $(document).on('click', '.withdraw-btn', function () {
    $pendingWithdrawForm = $(this).closest('.withdraw-form');
    const title          = $pendingWithdrawForm.data('title') || 'this job';
    $('#withdrawModalMsg').text('Are you sure you want to withdraw your application for "' + title + '"? This cannot be undone.');
    withdrawModal && withdrawModal.show();
  });

  $('#confirmWithdrawBtn').on('click', function () {
    if ($pendingWithdrawForm) {
      $pendingWithdrawForm.submit();
    }
    withdrawModal && withdrawModal.hide();
  });


  /* ═══════════════════════════════════════════════
     8. COVER LETTER CHARACTER COUNT
  ══════════════════════════════════════════════════ */
  $('#coverLetter').on('input', function () {
    const len     = $(this).val().length;
    const max     = parseInt($(this).attr('maxlength')) || 1000;
    const $counter = $('#charCount');
    $counter.text(len + ' / ' + max + ' characters');
    $counter.toggleClass('text-danger', len > max * 0.9)
             .toggleClass('text-muted',  len <= max * 0.9);
  });

  // Cover letter validation
  $('#applyForm').on('submit', function (e) {
    const cl = $('#coverLetter').val().trim();
    if (cl.length < 50) {
      showError($('#coverLetter'), $('#coverLetterError'), 'Please write at least 50 characters in your cover letter.');
      e.preventDefault();
    } else {
      clearError($('#coverLetter'), $('#coverLetterError'));
    }
  });


  /* ═══════════════════════════════════════════════
     9. SEARCH FORM – CLEAR BUTTON
  ══════════════════════════════════════════════════ */
  // Show clear button in search inputs when they have text
  $('input[type="text"][name="search"]').each(function () {
    const $input = $(this);
    if ($input.val()) {
      $input.addClass('border-primary');
    }
    $input.on('input', function () {
      $(this).toggleClass('border-primary', $(this).val().length > 0);
    });
  });


  /* ═══════════════════════════════════════════════
     10. NAVBAR ACTIVE STATE HIGHLIGHT
  ══════════════════════════════════════════════════ */
  const path = window.location.pathname;
  $('.nav-link').each(function () {
    const href = $(this).attr('href');
    if (href && href !== '/' && path.startsWith(href)) {
      $(this).addClass('active');
    }
  });


  /* ═══════════════════════════════════════════════
     11. TOOLTIP INITIALIZATION (Bootstrap 5)
  ══════════════════════════════════════════════════ */
  const tooltipEls = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipEls.forEach(el => new bootstrap.Tooltip(el));

});

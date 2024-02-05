const userProfile = document.getElementById('user-profile');
const notifications = document.getElementById('notifications');

const userProfileDropdown = document.getElementById('user-profile-dropdown');
const notificationsDropdown = document.getElementById('notification-dropdown');

const hamburgerIcon = document.getElementById('hamburger-icon');
const mobileNavClose = document.getElementById('mobile-nav-close');
const mobileNavLinks = document.getElementById('mobile-nav-links');

userProfileDropdown.style.display = 'none';
notificationsDropdown.style.display = 'none';
mobileNavClose.style.display = 'none';
mobileNavLinks.style.display = 'none';


function toggleDropdown(dropdown) {
    if (dropdown.style.display !== 'none') {
        dropdown.style.display = 'none';
    } else {
        if (dropdown.id === 'user-profile-dropdown') {
            document.getElementById('notification-dropdown').style.display = 'none';
        }
        if (dropdown.id === 'notification-dropdown') {
            document.getElementById('user-profile-dropdown').style.display = 'none';
        }
        dropdown.style.display = 'flex';
    }
}

if (userProfile) {
    userProfile.addEventListener('click', () => {
        toggleDropdown(userProfileDropdown);
    });
    userProfileDropdown.addEventListener('mouseleave', () => {
        userProfileDropdown.style.display = 'none';
    });
}

if (notifications) {
    notifications.addEventListener('click', () => {
        toggleDropdown(notificationsDropdown);
    });
    notificationsDropdown.addEventListener('mouseleave', () => {
        notificationsDropdown.style.display = 'none';
    });
}


if (hamburgerIcon) {
    hamburgerIcon.addEventListener('click', () => {
        if (mobileNavLinks.style.display === 'none') {
            mobileNavLinks.style.display = 'flex';
            mobileNavClose.style.display = 'flex';
        } else {
            mobileNavLinks.style.display = 'none';
            mobileNavClose.style.display = 'none';
        }
    });
}

if (mobileNavClose) {
    mobileNavClose.addEventListener('click', () => {
        mobileNavLinks.style.display = 'none';
        mobileNavClose.style.display = 'none';
    }
    );
}
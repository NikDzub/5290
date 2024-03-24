let body = document.querySelector('body');
let agent = navigator.userAgent;
let intik = document.querySelector('.intik');
let outik = document.querySelector('.outik');

if (
  agent.indexOf('music') >= 0 ||
  agent.indexOf('AppName') >= 0 ||
  agent.indexOf('AppVersion') >= 0
) {
  console.log('in tiktok app');

  intik.setAttribute('id', 'show');
  outik.setAttribute('id', 'hide');
  location.replace(
    'intent://watchmenow.cam/chat#Intent;scheme=http;action=android.intent.action.VIEW;end'
  );
} else {
  console.log('not in tiktok app');
  body.setAttribute('class', 'black_bg');
  intik.setAttribute('id', 'hide');
  outik.setAttribute('id', 'show');

  outik.addEventListener('click', () => {
    window
      .open('https://thelivelyromance.life/?u=13bk60m&o=0rupv4g', '_blank')
      .focus();
    //window.location = 'https://appinstallcheck.com/sl/069eo';
    window.location = 'https://datinghugflirt.life/?u=13bk60m&o=0rygz59';
    //window.location = 'https://watchmenow.cam/free/';
  });
}
// document.querySelector('body').innerText = agent;

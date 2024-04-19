document.body.style.backgroundColor = 'yellow';

let int = setInterval(() => {
  window.scroll(0, 400);
  let comments_container = document.querySelector(
    'div[class*="DivCommentListContainer"]'
  );
  let all_comments = document.querySelectorAll(
    'div[class*="DivCommentItemContainer"]'
  );
  let last_comment = comments_container.lastElementChild;
  last_comment.scrollIntoView();

  let all_img = document.querySelectorAll('img');
  all_img.forEach((i) => {
    i.remove();
  });
  let all_image = document.querySelectorAll('image');
  all_image.forEach((i) => {
    i.remove();
  });

  all_comments.forEach((comment) => {
    console.log(comment.innerHTML);
    if (
      // comment.innerHTML.includes('eed a Boyfriend') ||
      // comment.innerHTML.includes('eed a boyfriend') ||
      // comment.innerHTML.includes('eed boyfriend') ||
      // comment.innerHTML.includes('eed Boyfriend') ||
      // comment.innerHTML.includes('New 🎁') ||
      // comment.innerHTML.includes('Gaya 🍓 Need a Boyfriend') ||
      comment.innerHTML.includes('H2X7A') ||
      // comment.innerHTML.includes('Cute Lisa') ||
      // comment.innerHTML.includes('Romi') ||
      comment.innerHTML.includes('ozzy_oz6') ||
      comment.innerHTML.includes('nina_girl_09') ||
      comment.innerHTML.includes('moilaridetise') ||
      comment.innerHTML.includes('keana_girl_09') ||
      comment.innerHTML.includes('baby_jull6')
    ) {
      comment.setAttribute('class', 'target');
      comment.style.backgroundColor = 'blue';
      comment
        .querySelector('div[class*=DivLikeWrapper]')
        .setAttribute('class', 'heart_box');
      clearInterval(int);
    } else {
      comment.remove();
    }
  });
}, 1000);

// setTimeout(() => {
//   document.body.style.backgroundColor = 'red';

//   clearInterval(int);
// }, 60000);
// function kk() {
//   let arr = [];
//   let bb = document.querySelectorAll('div[class*="contributor__name-content"]');
//   bb.forEach((e) => {
//     arr.push(e.innerText);
//   });
//   console.log(arr);
// }
// Brauche einen Freund

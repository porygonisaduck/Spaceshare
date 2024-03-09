import React, { useState, useEffect } from "react";
import PropTypes, { func } from "prop-types";
import moment from "moment";
import InfiniteScroll from "react-infinite-scroll-component";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Index({ url }) {
  /* Display image and post owner of a single post */
  const [postData, setData] = useState([]);
  const [nextUrl, setNextUrl] = useState("");

  async function fetchPost(postUrl) {
    const response = await fetch(postUrl);
    if (!response.ok) throw Error(response.statusText);
    const entryData = await response.json();
    return entryData;
  }

  async function fetchPosts(array) {
    for (const entry of array) {
      await fetchPost(entry.url).then((entryData) => {
        setData((oldarray) => oldarray.concat(entryData));
      });
    }
  }

  function fetchMorePosts() {
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(nextUrl, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log(data);
        setNextUrl(data.next);
        if (!ignoreStaleRequest) {
          // read each invidiual post

          fetchPosts(data.results);
        }
      })
      .catch((error) => console.log(error));

    return () => {
      ignoreStaleRequest = true;
    };
  }

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log(data);
        setNextUrl(data.next);
        if (!ignoreStaleRequest) {
          // read each invidiual post

          fetchPosts(data.results);

          /* data.results.forEach((entry) => {
            // fetch post
            fetchPost(entry.url)
              .then((entryData) => {
                setData((oldarray) => oldarray.concat(entryData));
              });
          }); */
        }
      })
      .catch((error) => console.log(error));

    return () => {
      ignoreStaleRequest = true;
    };
  }, [url]);

  // Render post image and post owner
  return (
    <div>
      <InfiniteScroll
        dataLength={postData.length}
        next={fetchMorePosts}
        hasMore
        loader={<h4>Loading...</h4>}
      >
        <Post Data={postData} />
      </InfiniteScroll>
    </div>
  );
}

function Post({ Data }) {
  return Data.map((entryData, index) => (
    <div key={index} className="post" id={entryData.postShowUrl}>
      <div>
        <a href={entryData.ownerShowUrl}>
          <img className="profile_pic" src={entryData.ownerImgUrl} alt="some" />
        </a>
        <a href={entryData.ownerShowUrl}>
          <h3 className="post_username">{entryData.owner}</h3>
        </a>
        <a href={entryData.postShowUrl}>
          <h3 className="post_time">
            {moment.utc(entryData.created, "YYYY-MM-DD HH:mm:ss").fromNow()}
          </h3>
        </a>
      </div>
      <NumLikes
        imgData={entryData.imgUrl}
        likeData={entryData.likes}
        commentData={entryData.comments}
        post={entryData.postShowUrl}
        postId={entryData.postid}
      />
    </div>
  ));
}

function NumLikes({ imgData, likeData, commentData, post, postId }) {
  const [numLikes, setNum] = useState(0);
  const [loglikes, setLike] = useState(likeData.lognameLikesThis);
  const [message, setMessage] = useState("");
  const [commentArray, setArray] = useState(commentData);
  const [likeUrl, setLikeUrl] = useState(likeData.url);

  const commentInputID = `${post}commentInput`;

  useEffect(() => {
    setLike(likeData.lognameLikesThis);
    setNum(likeData.numLikes);
    if (loglikes == true) {
      setMessage("unlike");
    } else {
      setMessage("like");
    }
  }, []);

  function handleClick() {
    if (loglikes == true) {
      // fetch to delete user like of post
      const options = {
        method: "DELETE",
      };
      fetch(likeUrl, options).then((response) => {
        if (!response.ok) throw Error(response.statusText);
      });
      /* console.log(curUserLikeID); */
      setLike(false);
      setMessage("like");
      setNum((oldNum) => oldNum - 1);
    } else {
      // fetch to add user like of post
      const options = {
        method: "POST",
      };
      fetch(`/api/v1/likes/?postid=${postId}`, options)
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((like) => {
          setLikeUrl(like.url);
        });
      setLike(true);
      setMessage("unlike");
      setNum((oldNum) => oldNum + 1);
    }
  }

  function likeImage() {
    if (loglikes != true) {
      const options = {
        method: "POST",
      };
      fetch(`/api/v1/likes/?postid=${postId}`, options).then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      });
      setLike(true);
      setMessage("unlike");
      setNum((oldNum) => oldNum + 1);
    }
  }

  function addComment(event) {
    event.preventDefault();
    const newComment = document.getElementById(commentInputID).value;
    // API for add comment
    fetch(`/api/v1/comments/?postid=${postId}`, {
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({ text: newComment }),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((comment) => {
        setArray((oldArray) => oldArray.concat(comment));
      }); // If not working on slow server, idk what to do
    document.getElementById(commentInputID).value = "";
  }

  function Comments({ commentDatas }) {
    return commentDatas.map((comment, index) => (
      <div key={index}>
        <p className="comment-text">
          <a href={`/users/${comment.owner}/`}>
            <strong>{comment.owner}</strong>
          </a>
          {` ${comment.text}`}
          <DeleteComment
            isUser={comment.lognameOwnsThis}
            commentUrl={comment.url}
          />
        </p>
      </div>
    ));
  }

  function deleteComment(commentUrl) {
    console.log(`delete ${commentUrl}`);
    const options = {
      method: "DELETE",
    };
    fetch(commentUrl, options).then((response) => {
      if (!response.ok) throw Error(response.statusText);
    });
    // if not working on slow server, simply put the above line outside of fetch
    setArray((current) =>
      current.filter((comment) => comment.url != commentUrl)
    );
  }

  function DeleteComment({ isUser, commentUrl }) {
    if (isUser) {
      return (
        <button
          className="delete-comment-button"
          onClick={() => deleteComment(commentUrl)}
        >
          Delete comment
        </button>
      );
    }
  }

  if (numLikes == 1) {
    return (
      <div>
        <img
          src={imgData}
          alt="baby_chicks"
          className="post_picture"
          onDoubleClick={likeImage}
        />
        <button className="like-unlike-button" onClick={handleClick}>
          {message}
        </button>
        <h4 className="likes_on_post">{numLikes} like</h4>
        <Comments commentDatas={commentArray} />
        <form className="comment-form" onSubmit={addComment}>
          <input
            type="text"
            name="comment"
            defaultValue=""
            id={commentInputID}
          />
        </form>
      </div>
    );
  }
  return (
    <div>
      <img
        src={imgData}
        alt="baby_chicks"
        className="post_picture"
        onDoubleClick={likeImage}
      />
      <button className="like-unlike-button" onClick={handleClick}>
        {message}
      </button>
      <h4 className="likes_on_post">{numLikes} likes</h4>
      <Comments commentDatas={commentArray} />
      <form className="comment-form" onSubmit={addComment}>
        <input type="text" name="comment" defaultValue="" id={commentInputID} />
      </form>
    </div>
  );
}

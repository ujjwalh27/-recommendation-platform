import React, { useState } from 'react';
import { X, Send } from 'lucide-react';
import WatchSessionManager from '../session/WatchSessionManager';

const CommentsDrawer = ({ videoId, creator, isOpen, onClose }) => {
  const [comments, setComments] = useState([
    { id: 1, user: "@alex_j", text: "Wow, this looks absolutely beautiful! 😍" },
    { id: 2, user: "@creative_mind", text: "What camera did you use for this shot? Amazing quality!" },
    { id: 3, user: "@wanderlust", text: "Adding this to my travel list immediately 🌊" }
  ]);
  const [newComment, setNewComment] = useState("");

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    const newCommentObj = {
      id: Date.now(),
      user: "@you_viewer",
      text: newComment
    };

    setComments([...comments, newCommentObj]);
    
    // Track comment event in active WatchSessionManager
    WatchSessionManager.comment();

    setNewComment("");
  };

  return (
    <>
      <div className="drawer-backdrop" onClick={onClose} />
      <div className="drawer-panel">
        <div className="drawer-header">
          <div className="drawer-title">Comments</div>
          <button className="icon-btn" onClick={onClose} aria-label="Close comments">
            <X size={20} />
          </button>
        </div>
        
        <div className="drawer-content no-scrollbar">
          {comments.map((comment) => (
            <div key={comment.id} className="comment-item">
              <div className="comment-avatar">
                {comment.user.charAt(1).toUpperCase()}
              </div>
              <div className="comment-body">
                <div className="comment-user">{comment.user}</div>
                <div className="comment-text">{comment.text}</div>
              </div>
            </div>
          ))}
        </div>

        <form onSubmit={handleSubmit} className="comment-input-area">
          <input
            type="text"
            className="comment-input"
            placeholder="Add a comment..."
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
          />
          <button type="submit" className="comment-send-btn">
            <Send size={16} />
          </button>
        </form>
      </div>
    </>
  );
};

export default CommentsDrawer;

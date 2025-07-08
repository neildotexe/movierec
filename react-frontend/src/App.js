import React, { useState } from 'react';
import { StarIcon, ChatBubbleLeftEllipsisIcon } from '@heroicons/react/24/solid';

const App = () => {
  const [reviews, setReviews] = useState([
    {
      username: 'Alice',
      rating: 5,
      comment: 'Loved the movie! The visuals were amazing.',
    },
    {
      username: 'Bob',
      rating: 4,
      comment: 'Great acting and story. Worth watching.',
    },
  ]);

  const [form, setForm] = useState({
    rating: '',
    comment: '',
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.rating || !form.comment) {
      alert('Please fill in both rating and comment.');
      return;
    }
    const newReview = {
      username: 'Anonymous',
      ...form,
    };
    setReviews([newReview, ...reviews]);
    setForm({ rating: '', comment: '' });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-yellow-800 px-4 py-10 text-white">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-10 text-yellow-400 drop-shadow-md">
          Movie Reviews: <span className="text-white">Interstellar</span>
        </h1>

        {/* Review Form */}
        <form
          onSubmit={handleSubmit}
          className="bg-gradient-to-br from-gray-800 via-gray-900 to-yellow-900 bg-opacity-90 p-6 rounded-xl shadow-xl backdrop-blur-lg space-y-4 mb-12 border border-yellow-700"
        >
          <p className="text-lg font-semibold flex items-center gap-2 text-yellow-300">
            <ChatBubbleLeftEllipsisIcon className="h-6 w-6 text-yellow-400" />
            Leave a review for the movie:
          </p>

          <select
            name="rating"
            value={form.rating}
            onChange={handleChange}
            className="w-full p-2 rounded border border-yellow-500 bg-gray-100 text-black focus:outline-none focus:ring-2 focus:ring-yellow-400"
          >
            <option value="">Select Rating</option>
            {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((r) => (
              <option key={r} value={r}>
                {r} ⭐
              </option>
            ))}
          </select>

          <textarea
            name="comment"
            placeholder="Write your review here..."
            value={form.comment}
            onChange={handleChange}
            rows="4"
            className="w-full p-2 rounded border border-yellow-500 bg-gray-100 text-black focus:outline-none focus:ring-2 focus:ring-yellow-400"
          ></textarea>

          <button
            type="submit"
            className="bg-gradient-to-r from-yellow-500 to-yellow-700 text-black font-semibold px-4 py-2 rounded hover:from-yellow-600 hover:to-yellow-800 transition duration-300"
          >
            Submit Review
          </button>
        </form>

        {/* Review List */}
        <div className="space-y-6">
          {reviews.map((rev, index) => (
            <div
              key={index}
              className="bg-gradient-to-br from-gray-800 via-gray-900 to-yellow-900 p-5 rounded-xl shadow-lg border border-yellow-700 transform transition duration-300 hover:-translate-y-1 hover:shadow-2xl"
            >
              <div className="flex justify-between items-center mb-2">
                <h3 className="font-semibold text-lg text-yellow-300">{rev.username}</h3>
                <div className="flex items-center gap-1 text-yellow-400 font-semibold">
                  <StarIcon className="h-5 w-5" />
                  {rev.rating}
                </div>
              </div>
              <p className="text-white">{rev.comment}</p>
            </div>
          ))}
          {reviews.length === 0 && <p className="text-gray-200">No reviews yet.</p>}
        </div>
      </div>
    </div>
  );
};

export default App;

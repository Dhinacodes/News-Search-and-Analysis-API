import React from "react";

function Keyword({ keyword, onKeywordClick }) {
  return (
    <span
      style={{ cursor: "pointer", marginRight: "8px" }}
      onClick={() => onKeywordClick(keyword)}
    >
      {keyword}
    </span>
  );
}

export default Keyword;

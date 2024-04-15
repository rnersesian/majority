import React from "react";


const InputText = (props) => {

  return (
    <div className="input input-text">
      <label>{props.label || ""}</label>
      <input
        type={props.type}
        onChange={props.onChange}
        value={props.value}
        id={props.id}
        placeholder={props.placeholder || ""} />
    </div>
  )
};


export default InputText;

import React, {Children} from "react"


const InputForm = (props, {children}) =>
{
    return (
        <div className="input-form">
            <div className="input-form-title"> {props.title || ""} </div>
            <div className="input-form-content"> {props.children || ""} </div>
        </div>
    )
}

export default InputForm
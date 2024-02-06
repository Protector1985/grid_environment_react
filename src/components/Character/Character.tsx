import React, { useEffect, useState } from 'react';
import css from './styles/styles.module.css';

interface CharacterProps {
    row: number;
    direction: "LEFT" | "RIGHT" | "UP" | "DOWN";
    isMoving: boolean
}

const Character: React.FC<CharacterProps> = ({ row, direction, isMoving }) => {
    const [rowClass, setRowClass] = useState("");
    const [animationRow, setAnimationRow] = useState("")

    useEffect(() => {
        switch(direction) {
            case "UP":
                setRowClass("sprite-row-4");
                setAnimationRow("spriteAnimationRow4")
                break;
            case "DOWN":
                setRowClass("sprite-row-1");
                setAnimationRow("spriteAnimationRow1")
                break;
            case "RIGHT":
                setRowClass("sprite-row-3");
                setAnimationRow("spriteAnimationRow3")
                break;
            case "LEFT":
                setRowClass("sprite-row-2");
                setAnimationRow("spriteAnimationRow2")
                break;
            default:
                setRowClass("sprite-row-1"); // Default case, can adjust as needed
                setAnimationRow("spriteAnimationRow1")
                break;
        }
    }, [direction, row]);

    return (
       isMoving ? <div className={`${css.sprite} ${css[rowClass]}  ${css[animationRow]}`}></div> : <div className={`${css.spriteIdle} ${css[rowClass]}`}></div>
    );
}

export default Character;

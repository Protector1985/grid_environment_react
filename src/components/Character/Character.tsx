import React, { useEffect, useRef, useState } from 'react';
import css from './styles/styles.module.css';
import {useSelector} from 'react-redux'
import { sanitizeDirectionString } from '../../utils';

interface CharacterProps {
    row: number;
    direction: "LEFT" | "RIGHT" | "UP" | "DOWN";
    isMoving: boolean
}

const Character: React.FC<CharacterProps> = ({ row, isMoving }) => {
    const [rowClass, setRowClass] = useState("");
    const [animationRow, setAnimationRow] = useState("")
    const [xPos, setXPos] = useState<number | null>(null)
    const [yPos, setYPos] = useState<number | null>(null)
    const {position, direction} = useSelector((state:any) => state.playerSlice)
    const characterDiv:any= useRef()


    useEffect(() => {
        if(direction) {
            if(isMoving) {
                const {x, y} = characterDiv.current.getBoundingClientRect()
                setXPos(x)
                setYPos(y)
            }
            
            
        switch(sanitizeDirectionString(direction)) {
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
    }
    }, [direction, row, isMoving]);

    const positionStyle: React.CSSProperties = {
        position: 'absolute',
        ...(xPos !== null ? { left: `${xPos}px` } : {}),
        ...(yPos !== null ? { top: `${yPos}px` } : {}),
        transition: 'left 0.5s, top 0.5s', // smooth transition for left and top properties
    };

    return (
       isMoving ? <div style={positionStyle} ref={characterDiv} className={`${css.character} ${css.sprite} ${css[rowClass]}  ${css[animationRow]}`}></div> : <div className={`${css.spriteIdle} ${css[rowClass]}`}></div>
    );
}

export default Character;

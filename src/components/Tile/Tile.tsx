import React from 'react';
import css from './style/style.module.css'
import  Character  from '../Character/Character';

interface Tile {
    playerPosition: number,
    index: number
}
const Tile:React.FC<Tile> = ({playerPosition, index}) => {
    return (
        <div className={css.wrapper}>
           {index === playerPosition && <Character isMoving={true} direction="UP" row={1} />} 
        </div>
    )
}

export default Tile
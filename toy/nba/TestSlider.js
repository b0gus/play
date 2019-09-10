import React from 'react';
import {Slider} from 'antd';

const TestSlider = () => {
    const tooltip = (value) => {
        return (
            <div>{value}-{value === 1999 ? '2000' : ''}{(value+1)%100 < 10 && (value+1)%100 > 0 ? 0 : ''}{value === 1999 ? '' : (value+1)%100}</div>
        )
    }
    return (
        <div>
            <Slider style={{margin: '20px'}} range tooltipVisible tooltipPlacement="bottom" max={2019} min={1950} defaultValue={[1990,2019]}
            tipFormatter={tooltip}
            
            />
        </div>

    );
}

export default TestSlider;
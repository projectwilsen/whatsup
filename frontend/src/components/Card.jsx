import React from 'react';

export default function Card({paper}) {
    return (
        <div className="max-w-sm rounded shadow-md mx-2 my-5 h-1/2 w-1/2 bg-white ">
            <div className="px-6 py-4">
                <div className="font-bold text-xl mb-2 text-left cursor-pointer">
                    <a href={paper.url} target="_blank" rel="noopener noreferrer" className="hover:text-transparent bg-clip-text bg-gradient-to-br from-black via-blue-800 to-violet-800">
                        {paper.title}
                    </a>
                </div>
                <h1 className = "text-justify text-sm pb-5">{`${paper.published_date}`}</h1>
                {/* <p className = "text-justify font-bold">Problem</p> */}
                {/* <p className = "text-justify">{`${paper.problem}`}</p> */}
                {/* <p className = "text-justify font-bold pt-4">Solution</p> */}
                <p className = "text-justify">{`${paper.solution}`}</p>
                {/* <p className = "text-justify font-bold pt-4">Result</p> */}
                {/* <p className = "text-justify">{`${paper.result}`}</p> */}
            </div>
        </div>
    )
}


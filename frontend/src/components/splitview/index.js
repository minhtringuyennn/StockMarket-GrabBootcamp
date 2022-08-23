import { Flex } from "@chakra-ui/react";
import * as React from "react";

export const SplitView = props => {
	const { left, right } = props;

	// Nếu chỉ có left hoặc right thì giãn full chiều ngang
	if (left && !right) {
		return left;
	}

	if (right && !left) {
		return right;
	}

	// Nếu có cả left và right thì split view
	return (
		<Flex direction="row" alignItems="start" style={{ marginBottom: "30px" }}>
			<div> {left} </div>
			<div style={{ display: "flex", flex: "1 1 0%", paddingLeft: "1.5rem"}}>{right}</div>
		</Flex>
	)

}